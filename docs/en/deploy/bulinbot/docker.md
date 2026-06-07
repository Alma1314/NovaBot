# Deploy BulinBot with Docker

> [!WARNING]
> Docker provides a convenient way to deploy BulinBot on Windows, Mac, and Linux.
>
> This tutorial assumes you have Docker installed in your environment. If not, please refer to the [Docker official documentation](https://docs.docker.com/get-docker/) for installation.

## Deploy with Docker Compose

::: details Deploy BulinBot Only (General Method)

First, clone the BulinBot repository to your local machine:

```bash
git clone https://github.com/BulinBotDevs/BulinBot
cd BulinBot
```

Then, run Compose:

```bash
sudo docker compose up -d
```

> [!TIP]
> If your network environment is in mainland China, the above command will not pull properly. You may need to modify the compose.yml file and replace `image: soulter/bulinbot:latest` with `image: m.daocloud.io/docker.io/soulter/bulinbot:latest`.
:::

::: details Deploy with Agent Sandbox Environment

Supports native Python code execution, Shell code execution, and other features.

Deployment method:

```bash
git clone https://github.com/BulinBotDevs/BulinBot
cd BulinBot
# Modify the environment variable configuration in the compose-with-shipyard.yml file, such as Shipyard's access token, etc.
docker compose -f compose-with-shipyard.yml up -d
docker pull soulter/shipyard-ship:latest
```

For configuration and usage details, see the [Agent Sandbox Environment](/en/use/bulinbot-agent-sandbox.md) documentation.
:::


## Deploy with Docker

```bash
mkdir bulinbot
cd bulinbot
sudo docker run -itd -p 6185:6185 -p 6199:6199 -v $PWD/data:/BulinBot/data -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro --name bulinbot soulter/bulinbot:latest
```

> [!TIP]
> If your network environment is in mainland China, the above command will not pull properly. Please use the following command to pull the image:
>
> ```bash
> sudo docker run -itd -p 6185:6185 -p 6199:6199 -v $PWD/data:/BulinBot/data -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro --name bulinbot m.daocloud.io/docker.io/soulter/bulinbot:latest
> ```
>
> (Thanks to DaoCloud ❤️)

> No need to add sudo on Windows, same below
> Sync Host Time on Windows (requires WSL2)

```
-v \\wsl.localhost\(your-wsl-os)\etc\timezone:/etc/timezone:ro
-v \\wsl.localhost\(your-wsl-os)\etc\localtime:/etc/localtime:ro
```

View BulinBot logs with the following command:

```bash
sudo docker logs -f bulinbot
```

## 🎉 All Done

If everything goes well, you will see logs printed by BulinBot.

If there are no errors, you will see a log message similar to `🌈 Dashboard started, accessible at` with several links. Open one of the links to access the BulinBot dashboard.

> [!TIP]
> Since Docker isolates the network environment, you cannot use `localhost` to access the dashboard.
>
> New users must use the random password printed in the startup logs to log in for the first time. Use the username shown in the logs (usually `bulinbot`) and change the password after first login.
>
> If deployed on a cloud server, you need to open ports `6180-6200` and `11451` in the cloud provider's console.

Next, you need to deploy any messaging platform to use BulinBot on that platform.
