# pre:
# For NERSC: login to nerc docker registry: docker login registry.nersc.gov
# For polyneme: login to docker for polyneme using docker login

cp ../nmdco.owl . # owl needs to be in same dir

# login to docker registry
docker login registry.nersc.gov # for NERSC image
# docker login # for polyneme image

# build image
docker push registry.nersc.gov/m3408/nmdco # for NERSC image
# docker build -t polyneme/nmdco . # for polyneme image

# push image
docker push registry.nersc.gov/m3408/nmdco # for NERSC
# docker push polyneme/nmdco # push to polyneme

# After pushing to NERSC, login to http://rancher2.spin.nersc.gov
# and update to new image and redeploy
