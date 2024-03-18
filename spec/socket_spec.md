# Message types
The following message types will be used:

#### Client -> Server
- `command`


#### Server -> Client
- `ack_response`
- `feedback`
- `robot_state`

# Client sent -> Backend

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

## Undo
```json
{
  "type": "Undo",
  "data": {
    "id": 1
  }
}
```

# Server sent -> Client

---

## Response
```json
{
  "type": "Ack_response",
  "data": {
    "id": 1,
    "command": "set_digital_out(1,True)",
    "status": "Enum<Ok|Error>",
    "message": "optional message"
  }
}
```

## UndoResponse
```json
{
  "type": "Undo_response",
  "data": {
    "id": 1,
    "status": "Enum<Ok|Error|CommandDidNotExist|CommandAlreadyUndone>"
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
Payload is measured in kg mass. 
```json
{
  "type": "Robot_state",
  "data": {
    "safety_status": "reduced_mode",
    "runtime_state": "playing",
    "robot_mode": "running",
    "joints": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "tcp": {
      "pose": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      "speed": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      "force": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "payload": 0.0
  }
}
```


# Robot sent -> Backend

---

## Command finished
```json
{
  "type": "Command_finished",
  "data": {
    "id": 1,
    "command": "set_digital_out(1,True)",
    "variables": [
      {
        "name": "var1",
        "type": "Enum<string|int|float|bool|array|pose>",
        "value": "string|int|float|bool|array|pose"
      },
      {
        "name": "var2",
        "type": "Enum<string|number|bool|array|pose>",
        "value": "string|number|bool|array|pose"
      }
    ]
  }
}
```