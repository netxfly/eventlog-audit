#include <EventLog.au3>
#include <SQLite.au3>


_SQLite_Startup()	;Init sqllite library
Local $sDbName		; sqlite db name
$sDbname = "Eventlog.db"
Local $hDskDb = _SQLite_Open($sDbName)
local $sql
;$sql = "create table eventlog(id int not null, EventRecordID int, time text,EventID int,Level int,log_type text,Provider text,Computer text, user text,eventdata text,PRIMARY KEY (`id`))"
$sql = "create table eventlog(EventRecordID int, time text,EventID int,Level int,log_type text,Provider text,Computer text, user text,eventdata text)"
ConsoleWrite(_SQLite_Exec($hDskDb, $sql))

;Start to dump Log
dumplog($hDskDb, "system")
dumplog($hDskDb, "Application")
dumplog($hDskDb, "Security")
;End of dump Log;
_SQLite_Shutdown()		;shutdown sqlite library

;Dump log function
Func dumplog($hDskDb, $logname)
   ;定义变量
   Local $hEventLog	; 事件日志文件句柄
   Local $aEvent		; 日志array
   Local $nEventCount	; 日志条目
   Local $szIPADDRESS	; IP地址

   $szIPADDRESS = @IPAddress1
   $hEventLog = _EventLog__Open("", $logname)
   $nEventCount =  _EventLog__Count($hEventLog)
   ConsoleWrite($nEventCount)

   For $ioffset = 0 To $nEventCount - 1 Step 1
	  $aEvent = _EventLog__Read($hEventLog)
	  ;ConsoleWrite($aEvent)
	  ;ConsoleWrite(UBound($aEvent)) ;array size :15

	  For $i = 0 to UBound($aEvent) -1 Step 1
		 ConsoleWrite($aEvent[$i] & "|")
		 Local $EventRecordID = $aEvent[1]
		 Local $time = $aEvent[2] & " " & $aEvent[3]
		 Local $EventID = $aEvent[6]
		 Local $Level = $aEvent[7]
		 Local $log_type = $aEvent[8]
		 Local $Provider = $aEvent[10]
		 Local $Computer = $aEvent[11]
		 Local $user = $aEvent[12]
		 Local $eventdata = $aEvent[13]
	  Next
	  local $sql = "insert into eventlog values(" & $EventRecordID & ",'" & $time & "'," &  $EventID & "," & $Level & ",'" & $log_type & "','" & $Provider & "','" & $Computer & "','" & $user & "','" & $eventdata & "')"
	  ;ConsoleWrite($sql)
	  ConsoleWrite(_SQLite_Exec($hDskDb, $sql))
	  
	  ConsoleWrite(@CRLF & "--------------------------------" & @CRLF)
   Next
   _EventLog__Close($hEventLog)
EndFunc