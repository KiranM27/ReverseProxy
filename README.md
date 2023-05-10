# Reverse Proxy

This repository contains a reverse proxy server that acts as an intermediary between client devices and backend servers. It helps enhance performance, scalability, security, and flexibility in your web architecture.

## Setup

To use this reverse proxy, you need to update the following variables in the `constants.py` file:

```python
DESTINATION_DOMAIN = "backend.treehopper.finance"
REVERSE_PROXY_HOST = "0.0.0.0"
REVERSE_PROXY_PORT = 8080
```

- `DESTINATION_DOMAIN`: Specify the domain or IP address of your backend server. Replace `"backend.treehopper.finance"` with the appropriate value.

- `REVERSE_PROXY_HOST`: Set the host IP address where the reverse proxy server will run. By default, it is set to `"0.0.0.0"`, which means it will listen on all available network interfaces.

- `REVERSE_PROXY_PORT`: Define the port number for the reverse proxy server. The default value is `8080`, but you can change it if needed.

## Usage

1. Clone this repository to your local machine.

```shell
git clone https://github.com/your-username/reverse-proxy.git
```

2. Update the variables mentioned above in the `constants.py` file.

3. Install the required dependencies.

```shell
pip install -r requirements.txt
```

4. Start the reverse proxy server.

```shell
python reverse_proxy.py
```

The reverse proxy will now be running and listening for incoming client requests.
