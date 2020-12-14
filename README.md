#### Requirements:
- Python version must be 3.6 or higher (we use f-strings)
- Code must be run from root of 'Lightning Network Analysis' directory
- If the code fails, you likely don't have some of the dependencies installed. Run the code commands 
below to install all dependencies
- `python` is an alias for your route to your python executable. Something like `/usr/local/bin/python3.8` 


```
python -m pip install -r requirements.txt
```

#### Notes:
- This program was written to help as an adjunct part of the our final project to help us better understand the
structure of the lightning network. It is not our entire project. We recommend that just use option 0 when running 
the main function, but you are free to try out the other options as well.
- Loading and parsing information from the available API is time consuming due to the fact that we are not loading in 
bulk. It may be more efficient to use some of the command is the curl section to collect bulk data. 
- the `pickles` directory store all of the saved pickles that the program uses

#### Running the Main Function:
- run `python main`
- then enter the public keys for the nodes you want to route between
- enter the amount in satoshi you want to route
- choose your graph edge weight metric to be hop distance, or transaction fees
  - Hop Distance: all edges have equal weight
  - Cost: edge weights are determined by the call
- choose your routing algorithm
  - Shortest Path: Find the shortest path from source to target
  - Extra Loops: Add extra loops between intermediate nodes on the path from source to target
  - Random Routing: Randomly select two nodes which much be on the route from source to target.

#### Calling APIs from command line:
- We use two main base endpoints for API calls
  - `https://explorer.acinq.co/` collects information from the Lightning Network Explorer
  - `https://ln.bigsun.xyz/api/` collects live node and channel information from an existing API
- Sample commands to collect information
  - `curl 'https://explorer.acinq.co/nodes'` collects all nodes from the explorer
  - `curl 'https://explorer.acinq.co/channels'` collects all channels from the explorer
  - `curl 'https://ln.bigsun.xyz/api/nodes?pubkey=eq.<pubkey1>'` collects node information for node with public key `<pubkey1>`
  - `curl 'https://ln.bigsun.xyz/api/nodes?pubkey=in.(<pubkey1>,<pubkey2>,<pubkey3>,...)'` collects node information for node with public key in the list `(<pubkey1>,<pubkey2>,<pubkey3>,...)`
  - `curl 'https://ln.bigsun.xyz/api/channels?short_channel_id=eq.<channelId1>'` collects channel information for channel with id `<channelId1>`
  - `curl 'https://ln.bigsun.xyz/api/policies?short_channel_id=eq.<channelId1>'` collects channel policies for channel with id `<channelId1>`. This contains information like base and rate fees.
  - `curl 'https://ln.bigsun.xyz/api/rpc/node_channels?pubkey=eq.<pubkey1>'` collects information about node with public key `<pubkey1>` as well as information/policies about all channels involving this node. This is useful for developing an adjacency list graph. 
  - Go to https://ln.bigsun.xyz/docs to see more information about the specific API
  - Go to https://postgrest.org/en/v7.0.0/api.html to see more information about querying postgREST API