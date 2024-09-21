# Whitelist
A Plugin plugin in Python for Endstone

## Usage
create folder in dir /plugins/configuration/whitelist


than in this folder create file config.json
this file should have this fields

```json
{
    "profile": "<profile name>"
}
```
and then u need to create file \<profile name\>.json with this fields

```json
[
    "<your nickname in mc>"
]
```

plugin also contains commands such as

/wl add - \<name\> adds user to whitelist

/wl remove - \<name\> removes user from whitelist

/wl profile - \<name\> set profile to use

/wl view - shows all users that are in used profile

/wl check - check players that are online and if they are not in whitelist kicks them usually used after profile change 