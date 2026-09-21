# Maintain.ai IoT Device Contract

The IoT Gateway is a device connectivity layer. It is not a user client.

## Identity

The gateway authenticates telemetry with:

`X-Device-Key: <machine-device-key>`

The device key resolves to a specific machine on the Maintain.ai backend. The gateway must not use worker or engineering JWTs for telemetry ingestion.

## Ingestion

Current ingestion endpoint:

`POST /api/devices/ingest`

The configured API URL may be supplied through:

`MAINTAIN_AI_API_URL`

Keep the endpoint configurable so backend hosting can change without rebuilding the gateway.

## Canonical telemetry

A submitted reading contains:

`reading_type`
`value`
`unit`
`event_id`
`recorded_at`

The gateway generates an event ID when the source does not provide one. Event IDs allow retry-safe ingestion.

## Offline delivery

Temporary network/server failures may be queued locally in SQLite. Successful delivery or an idempotent conflict removes the event from the queue.

Permanent authentication or validation failures must not remain in the queue forever.

## Machine and organization scope

The gateway should only know the device key and local pairing information needed to operate the paired machine. Organization authorization is resolved by the backend through the machine/device relationship.

## Sensor validation

Local validation is a safety and quality filter, not the final authority. The backend must validate incoming telemetry again.

## Do not add

Do not store user passwords, worker tokens, organization-wide credentials, or hard-coded organization IDs in the gateway.
