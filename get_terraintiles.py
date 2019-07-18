
import os
import elevation

# create out folder
out_path = os.path.join(os.getcwd(), "tmp")
os.makedirs(out_path, exist_ok=True)

# Because we can't request large areas all at once,
# loop through 1 degree tiles along 49th parallel
for i, xmin in enumerate(range(-123, -113)):
    output = os.path.join(out_path, 'mapzen_{}.tif'.format(i))
    elevation.clip(bounds=(xmin, 48, xmin + 1, 49.1), output=output)

# clean up stale temporary files and fix the cache in the event of a ver error
elevation.clean()
