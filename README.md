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
       -F 'file=@sample.m4a;type=audio/x-m4a'    \
       -o output.mp3
       ```

## TODO
- [ ] Lyrics will be sub titled.
- [ ] Basic visualization will be added for fun.
