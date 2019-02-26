box.cfg {
    listen = 3301,
    replication = {
        'replicator:$uGRsV4anu*9x%FZ@tarantool-master:3301',
        'replicator:$uGRsV4anu*9x%FZ@tarantool-replica:3301'
    },
    read_only = false
}

box.once('bootstrap', function()
    box.schema.space.create('shortener')
    box.space.shortener:format({
        {name = 'id', type = 'integer'},
        {name = 'url', type = 'string'},
        {name = 'expires', type = 'integer'}
    })

    box.schema.sequence.create('shortener', {min = 0})
    box.space.shortener:create_index('primary', {sequence = 'shortener'})

    box.schema.user.create('tarantool', {password = 'kdCm!u=8As396FF4'})
    box.schema.user.grant('tarantool', 'read,write', 'space', 'shortener')
    box.schema.user.grant('tarantool', 'read', 'space', '_index')
    box.schema.user.grant('tarantool', 'read', 'space', '_space')
    box.schema.user.grant('tarantool', 'write', 'sequence', 'shortener')

    box.schema.user.create('replicator', {password = '$uGRsV4anu*9x%FZ'})
    box.schema.user.grant('replicator', 'replication')
end)


expirationd = require('expirationd')

local function is_expired(args, tuple)
  return tuple[3] < os.time()
end

local function delete_tuple(space_id, args, tuple)
  box.space[space_id]:delete{tuple[1]}
end

expirationd.start('clean_shortener', box.space.shortener.id, is_expired, {
    process_expired_tuple = delete_tuple, args = nil,
    tuples_per_iteration = 50, full_scan_time = 3600, force = true
})
