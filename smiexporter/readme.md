# Service Mesh Images exporter for installing RedHat Service Mesh in disconnected mode


### Export images automatically with `smiexporter.py` script
The `smiexporter.py` scripts may assist you to export RH Service Mesh images (Istio) from `registry.access.redhat.com` and import them to your
own private registry. 

***Important***
1. The `smiexporter.py` script will work only with Python3
2. Each command can be executed with `--dry-run true` flag, so commands will be just printed and not executed

Execute following steps to pull, tag and push the Service Mesh images 
1. Login to RH docker registry `docker login registry.access.redhat.com`, if you already logged in, skip this step.
2. Pull all RH Service Mesh docker images by executing `./smiexporter.py fetch`
3. Tag the images with your own private registry by executing `./smiexporter.py tag --registry docker.io/dimssss`
4. Push the tagged images to your own private registry by executing `./smiexporter.py push --registry docker.io/dimssss` 

### Export images manually
1. To get the list of all images do  `./smiexporter.py show  | awk '{print $4}'` or open in any text editor the `smiexporter.py` file and look for the `IMAGES` list. 
2. Tag each image in the list with your private registry address. For example:
      - The original image is `registry.access.redhat.com/openshift-istio-tech-preview/citadel:0.5.0` 
      - Private docker repo `docker.io/dimssss`
      - The docker tag should be as following: `docker tag registry.access.redhat.com/openshift-istio-tech-preview/citadel:0.5.0 docker.io/dimssss/citadel:0.5.0`. ***Note, when you are tagging image the last part should be always stay unchanged, in our example `citadel:0.5.0` will be the same, but the `registry.access.redhat.com/openshift-istio-tech-preview/` changed to `docker.io/dimssss/`***
3. Push tagged images to the private docker registry.