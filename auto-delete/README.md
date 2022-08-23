# Auto Delete

*Auto-delete is a light-weight Kyber Modmail plugin that deletes messages from users when they leave. This is useful for __advertising/promotions servers__ (or for servers that have a promotion channel) to enforce a rule that when users leave, their advertisements will be deleted.*

# Installation
> Make sure to replace `<prefix>` with your bot's prefix.
```
<prefix>plugins add Nzii3/modmail-plugins/auto-delete
```
**Example**
```
?plugins add Nzii3/modmail-plugins/auto-delete
```

# Getting Started

**1.** Setup your server's auto-delete limit:
> Make sure to replace `<prefix>` with your bot's prefix.
```
<prefix>autodelete limit <limit>
```
**Example**
```
?autodelete limit 100
```
This will search through 100 messages (default) in every set channel and delete messages if they are by the member that left.

---

**2.** Set auto-delete channels. These channels will be searched through to find messages to delete when a member leaves. *This would most likely be your server's advertising channel(s).*

> Make sure to replace `<prefix>` with your bot's prefix.
```
<prefix>autodelete add_channel <#channel>
```
**Example**
```
?autodelete add_channel #self-promotion
```

**2.1** To remove an auto-delete channel, use the following command
> Make sure to replace `<prefix>` with your bot's prefix.
```
<prefix>autodelete remove_channel <#channel>
```
**Example**
```
?autodelete remove_channel #self-promotion
```

# Credits
*Made with 💙 by [vNziie--#7777](https://nziie.is-a.dev)*
