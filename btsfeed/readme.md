requirement:
python version >=3.4
or python3 + module statistics

how to use this script?

1. run client with rpc enable, you can execute with a parameter like this:

      ./bitshares_client  --server --httpport 9989 --rpcuser user --rpcpassword pass

  or edit the config.json  like this:

      "rpc": {
        "enable": true,
        "rpc_user": "user",
        "rpc_password": "pass",
        "rpc_endpoint": "127.0.0.1:0",
        "httpd_endpoint": "127.0.0.1:9989",
        "htdocs": "./htdocs"
       },

2. cp config-sample.json to config.json

    edit the rpc parameter, delegate-list ...
    it's better to change market_weight 

3. if you just want to watch the price, run command without parameter

    ./bts_feed_auto.py 

4. if you want to publish feed,run command with the asset lists, like:

   ./bts_feed_auto.py USD CNY GLD


5. if there're multiple delegates for price feed publishing, script will randomly pick half number of delegates to publish feed each time