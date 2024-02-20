# Message types
The following message types will be used:

#### Client -> Server
- `command`


#### Server -> Client
- `ack_response`
- `feedback`
- `robot_state`

# Client sent

---

## Command
This is used for sending a command to the server. 
The server will respond with an `ack_response` message.
```json
{
  "type": "Command",
  "data": {
    "id": 1,
    "command": "set_digital_out(1,True)"
  }
}
```

# Server sent

---

## Response
```json
{
  "type": "Ack_response",
  "data": {
    "id": 1,
    "command": "set_digital_out(1,True)",
    "status": "ok or error",
    "message": "optional message"
  }
}
```


## Feedback
```json
{
  "type": "Feedback",
  "data": {
    "id": 1,
    "message": "message"
  }
}
```

## Robot state
```json
{
  "type": "Robot_state",
  "data": {
    "state": "running",
    "joints": [0, 0, 0, 0, 0, 0]
  }
}
```
