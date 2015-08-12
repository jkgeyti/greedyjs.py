## Greedyjs.py 
*... and how to download geo features from google maps*

### About

`greedyjs.py` is a simple little script that will try and extract usuable js/json from a webpage. You specify that start of some variable you're interested in, `greedyjs.py` finds that somewhere in the page, and greedily outputs characters from that point, until it believes the construct is fully defined.

## Examples

#### file

```
<some invalid html or whatever ...
var a = { "a" +
    "b", [1,2,
    3]}; anotherFuncton()
</script>
```

#### Extracting javascript

```bash
$ cat file | python greedyjs.py "var a ="
var a = { "a" +
    "b", [1,2,
    3]};
```

#### Extracting values only

```bash
$ cat file | python greedyjs.py "var a =" true
{ "a" +
    "b", [1,2,
    3]}
```

## Downloading geo regions from google

When searching Google Mapmaker, nicely formatted JSON is returned for any regions shown on the map, which is easily converted into e.g. geoJSON.

Let us download the region seen by on [http://www.google.co.uk/mapmaker?q=London,%20UK](http://www.google.co.uk/mapmaker?iwloc=0_0&fmi=0_0&gw=39&fid=5177063743470363247:3454669810191362443&dtab=overview&ll=51.48931,-0.08819&spn=0.510065,1.40625&z=11&lyt=large_map_v3&htll=54.978252,-1.61778&hyaw=90). In this example, we'll use `curl` to fetch the website, and use [`jq`](http://stedolan.github.io/jq/) to further postprocess the data returned by `greedyjs.py`:

```bash
$ curl -L --data-urlencode "q=Greater London" "http://www.google.co.uk/mapmaker" 2> /dev/null | \
  python greedyjs.py "window.geowiki.gHomeVPage" true | \
  jq ".overlays.polygons"
[{"id":"0_0","polylines":[{"id":"0_0","point":[{"lat":51.4680871,"lng":-0.5103751},{"lat":51.4675044,"lng":-0.5102962} ...
```