# Will Wood Wordle 🐀

Will Wood Wordle (a.k.a. WWWordle) is a fork from [this Wordle clone](https://github.com/cwackerfuss/react-wordle). 
* Built with React, Typescript, and Tailwind.
* Hosted with [Linode](https://www.linode.com/).

[**Play it here!**](http://45.56.82.31/)

## Build and run

### To Run Locally:

Clone the repository and perform the following command line actions:

```bash
$> cd react-wordle
$> npm install
$> npm run start
```

### To build/run docker container:

#### Development

```bash
$> docker build -t reactle:dev -f docker/Dockerfile .
$> docker run -d -p 3000:3000 --name reactle-dev reactle:dev
```

Open [http://localhost:3000](http://localhost:3000) in browser.

#### Production

```bash
$> docker build --target=prod -t reactle:prod -f docker/Dockerfile .
$> docker run -d -p 80:8080  --name reactle-prod reactle:prod
```

### To stop and remove prod container:
```bash
$> docker stop reactle-prod
$> docker rm reactle-prod
```
