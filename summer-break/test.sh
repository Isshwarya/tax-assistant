# simple curl test of 2 endpoints assuming default port for Flask, adjust as needed
curl -L -X POST http://127.0.0.1:8020/transactions/  -F "data=@summer-break/data.csv"
echo
curl -L http://127.0.0.1:8020/report/
