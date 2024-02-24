# Palworld UUID fix

This projects implements suggestion on this thread: https://github.com/xNul/palworld-host-save-fix/issues/158  
This tool should provide less invasive way to transfer host (and any other player) save to another player.  


The existing method from https://github.com/xNul/palworld-host-save-fix created unwanted bugs such as [Left click issue](https://github.com/xNul/palworld-host-save-fix), pals that do not work, new guid character need to be at least level 2 etc..  

## Usage

⚠️ Keep a backup copy of your save ⚠️  

### Step 1: Finding new character UUID
- Copy your desired save's folder from `C:\Users\<username>\AppData\Local\Pal\Saved\SaveGames\<random_numbers>` to `PalServer\Pal\Saved\SaveGames\0`.

- In the `PalServer\Pal\Saved\Config\WindowsServer\GameUserSettings.ini` file, change the DedicatedServerName to match your save folder's name. For example, if your save folder's name is `2E85FD38BAA792EB1D4C09386F3A3CDA`, the DedicatedServerName changes to `DedicatedServerName=2E85FD38BAA792EB1D4C09386F3A3CDA`.

- Run the dedicated server and confirm you can connect to your save on the dedicated server and that the world is the one you want. Upon entering the server will ask you to create a new character. (The server thinks you are a new player, instead of host)
   
- The co-op host must create a new character on the dedicated server. A new .sav file should appear in `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Players\`.
The name of that new .sav file is the co-op host's new GUID. We will need the co-op host's new GUID for the script to work.  

### Step 2: Overwrite new UUID into old save files 
- Copy `0000...000000000000000000001.sav` file and Level.sav file from the original save folder and copy it into a temporary directory.

- Install this script (Need Python)
`pip install palworld-fix-uuid`  

- Run script on these two files:
  
```bash 
# first file
palworld-fix-uuid --file-path "{path to 0000...0001.sav}" --to-uuid {NEW UUID}  

# second file
palworld-fix-uuid --file-path "{path to Level.sav}" --to-uuid {NEW UUID}  
```  

Check the output folder.  


### Step 3: Rename UUID updated old save files and move it to the dedicated server save folder.

- Change the first filename to {NEW UUID}.sav and second filename to {Level.sav}

Overwrite these two files to the dedicated server's save folder.  
first file: `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Players\{New UUID}.sav`  
second file: `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Level.sav`  

Note that you can also use this script to recover lost other player's save file too if they happen to corrupt the save files on their pc. (Using the host computer's player save file). This time you also need to specify --from-uuid argument in the script.  

- [Optional] remove old 00...0001.sav from `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Players\`

- Your new dedicate server should now correctly map your new character UUID and your existing save file.


## How to transfer co-op save to dedicated server (As of 2024/2/25)

I recommend SteamCMD so that you can unbind your steam account from the dedicated server (so that you can use another pc)  

Install SteamCMD:
https://developer.valvesoftware.com/wiki/SteamCMD  

Open CMD and run the following command:  

```bash
steamcmd +login anonymous +app_update 2394010 validate +quit  
```

Create a text file and change name to run_palworld_server.bat to improves performance in multi-threaded CPU environments.  
(Change path to PalServer if required):
```
C:\Steam\steamapps\common\PalServer/PalServer.exe EpicApp=PalServer -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS  
```  
For more information on the options: https://tech.palworldgame.com/settings-and-operation/arguments/  


Update steamapps\common\PalServer\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini  

For normal difficulty: (Or copy values from steamapps\common\PalServer\Pal\DefaultPalWorldSettings.ini)  
```
[/Script/Pal.PalGameWorldSettings]  

OptionSettings=(Difficulty=None,DayTimeSpeedRate=1.000000,NightTimeSpeedRate=1.000000,ExpRate=1.100000,PalCaptureRate=1.300000,PalSpawnNumRate=1.000000,PalDamageRateAttack=1.000000,PalDamageRateDefense=1.000000,PlayerDamageRateAttack=1.000000,PlayerDamageRateDefense=1.000000,PlayerStomachDecreaceRate=0.100000,PlayerStaminaDecreaceRate=1.000000,PlayerAutoHPRegeneRate=1.000000,PlayerAutoHpRegeneRateInSleep=1.000000,PalStomachDecreaceRate=0.100000,PalStaminaDecreaceRate=1.000000,PalAutoHPRegeneRate=1.000000,PalAutoHpRegeneRateInSleep=1.000000,BuildObjectDamageRate=1.000000,BuildObjectDeteriorationDamageRate=0.100000,CollectionDropRate=1.200000,CollectionObjectHpRate=1.000000,CollectionObjectRespawnSpeedRate=1.100000,EnemyDropItemRate=1.200000,DeathPenalty=None,bEnablePlayerToPlayerDamage=False,bEnableFriendlyFire=False,bEnableInvaderEnemy=True,bActiveUNKO=False,bEnableAimAssistPad=True,bEnableAimAssistKeyboard=False,DropItemMaxNum=3000,DropItemMaxNum_UNKO=100,BaseCampMaxNum=128,BaseCampWorkerMaxNum=15,DropItemAliveMaxHours=1.000000,bAutoResetGuildNoOnlinePlayers=False,AutoResetGuildTimeNoOnlinePlayers=72.000000,GuildPlayerMaxNum=20,PalEggDefaultHatchingTime=50.000000,WorkSpeedRate=2.000000,bIsMultiplay=False,bIsPvP=False,bCanPickupOtherGuildDeathPenaltyDrop=False,bEnableNonLoginPenalty=True,bEnableFastTravel=True,bIsStartLocationSelectByMap=True,bExistPlayerAfterLogout=False,bEnableDefenseOtherGuildPlayer=False,CoopPlayerMaxNum=10,ServerPlayerMaxNum=32,ServerName="Default Palworld Server",ServerDescription="Server",AdminPassword="",ServerPassword="",PublicPort=8211,PublicIP="",RCONEnabled=False,RCONPort=25575,Region="",bUseAuth=True,BanListURL="https://api.palworldgame.com/api/banlist.txt")  
```

to set "hard" difficulty on the dedicated server: (As of now, Difficulty=None does nothing)  
source: https://www.reddit.com/r/Palworld/comments/19coabg/how_to_set_hard_difficulty_for_dedicated_servers/  

```
[/Script/Pal.PalGameWorldSettings]  
OptionSettings=(Difficulty=None,DayTimeSpeedRate=1.000000,NightTimeSpeedRate=1.000000,ExpRate=0.800000,PalCaptureRate=0.800000,PalSpawnNumRate=1.000000,PalDamageRateAttack=1.000000,PalDamageRateDefense=1.000000,PlayerDamageRateAttack=0.500000,PlayerDamageRateDefense=4.000000,PlayerStomachDecreaceRate=1.000000,PlayerStaminaDecreaceRate=1.000000,PlayerAutoHPRegeneRate=1.000000,PlayerAutoHpRegeneRateInSleep=1.000000,PalStomachDecreaceRate=1.000000,PalStaminaDecreaceRate=1.000000,PalAutoHPRegeneRate=1.000000,PalAutoHpRegeneRateInSleep=1.000000,BuildObjectDamageRate=1.000000,BuildObjectDeteriorationDamageRate=1.000000,CollectionDropRate=0.500000,CollectionObjectHpRate=1.000000,CollectionObjectRespawnSpeedRate=1.000000,EnemyDropItemRate=0.500000,DeathPenalty=All,bEnablePlayerToPlayerDamage=False,bEnableFriendlyFire=False,bEnableInvaderEnemy=True,bActiveUNKO=False,bEnableAimAssistPad=True,bEnableAimAssistKeyboard=False,DropItemMaxNum=3000,DropItemMaxNum_UNKO=100,BaseCampMaxNum=128,BaseCampWorkerMaxNum=15,DropItemAliveMaxHours=1.000000,bAutoResetGuildNoOnlinePlayers=False,AutoResetGuildTimeNoOnlinePlayers=72.000000,GuildPlayerMaxNum=20,PalEggDefaultHatchingTime=72.000000,WorkSpeedRate=1.000000,bIsMultiplay=False,bIsPvP=False,bCanPickupOtherGuildDeathPenaltyDrop=False,bEnableNonLoginPenalty=True,bEnableFastTravel=True,bIsStartLocationSelectByMap=True,bExistPlayerAfterLogout=False,bEnableDefenseOtherGuildPlayer=False,CoopPlayerMaxNum=4,ServerPlayerMaxNum=32,ServerName="Default Palworld Server",ServerDescription="",AdminPassword="",ServerPassword="",PublicPort=8211,PublicIP="",RCONEnabled=False,RCONPort=25575,Region="",bUseAuth=True,BanListURL="https://api.palworldgame.com/api/banlist.txt")  
```

Update publicIP, AdminPassword, ServerPassword.  
If you do not want to expose your public IP, use VPN service like nordVPN.  

Meshnet example: (Use meshnet IP instead of your public IP)  
https://meshnet.nordvpn.com/how-to/gaming/palworld-dedicated-server  



## Firewall and Port forwarding
Follow step 4 and 5 from the link below:  
https://www.reddit.com/r/Palworld/comments/1abtxw5/psa_how_i_got_my_dedicated_server_working_steam/  


Now all players should be able to join the server with their existing characters except your character.  
Follow the script's usage guide to replace character UUID from 000...0001.sav to the host's new charater UUID.  