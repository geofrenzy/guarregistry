# Global Unmanned Airframe Registry (GUAR) Delegate

This project provides a kit for hosting a delegating GUAR server to register and retrieve information about unmanned airframes.
The server employs Docker and PowerDNS, and offers the modularity of Docker containers without sacrificing the sophistication of its DNS capabilities.

## Building and use
Before you begin, you should insert your API keys where appropriate.
The places to put your API key can be found like so:
```bash
grep -r "PlE@seChAnG3MeT0Some+hingEl$e" .
```
This workflow will be cleaned up in the future.

Once your API keys are in plate, to use this project from the command line, simply `cd` into `server` and call `sh delegate.sh`. To do important initial configuration on the server, you'll need to use the included toolkit under `tools`, which has its own README for more information.

In short, it should look something like this:
```bash
# Creating the server
cd server
sh delegate.sh
cd ../

# Configuring the server
cd tools
python3 setupdelegate.py
```
And at that point, you should begin to see prompts asking you for the information necessary to complete this process.

After you complete the prompts, your GUAR server will be ready to register airframes and handle requests.

(Note: Please change the default API key in both the server and the tools.)

