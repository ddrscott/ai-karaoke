# AI Karaoke

A web service to create karaoke tracks given any audio source.

The track is split between vocals and instruments.
The vocal track is the moved to the left audio channel and the instruments the right.


## Endpoints
- `POST /mp3`
   + returns audio only
   + Example use:

       ```
       curl -X POST 'http://localhost:8080/mp3/' \
       -H 'Content-Type: multipart/form-data'    \
       -F 'file=@sample.ogg;type=audio/x-ogg'    \
       -o output.mp3
       ```

## TODO
- [ ] Lyrics will be sub titled.
- [ ] Basic visualization will be added for fun.


## Installation

**Warning** There be demons. This is tricky if you're on OSX because of `spleeter` and it's use of an older Tensorflow. It's best to run this is Linux Docker.

We have this deployed Google Cloud Run using the provided Dockerfile.

```sh
docker build . -t ai-karaoke

docker run -it --rm -v ${PWD}:/app -p 8080:8080 ai-karaoke

curl -X POST 'http://localhost:8080/mp3/'   \
  -H 'Content-Type: multipart/form-data'    \
  -F 'file=@sample.ogg;type=audio/x-ogg'    \
  -o output.mp3
