#!/bin/bash

set -eu

docker-compose down
docker-compose up -d

cat <<EOF | docker-compose exec -T tarantool console
box.schema.space.create('shortener')
box.space.shortener:format({
    { name = 'id', type = 'integer' },
    { name = 'url', type = 'string' },
    { name = 'created', type = 'number' }
})
box.schema.user.grant('tarantool', 'write', 'space', 'shortener')
box.schema.sequence.create('shortener_seq', {min = 0})
box.space.shortener:create_index('primary', { sequence = 'shortener_seq' })
EOF

docker-compose logs -f
