# Auto Delete

*Auto-delete is a light-weight Kyber Modmail plugin that deletes messages from users when they leave. This is useful for __advertising/promotions servers__ (or for servers that have a promotion channel) to enforce a rule that when users leave, their advertisements will be deleted.*

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
