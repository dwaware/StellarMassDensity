display_height = 1000
# in pixels

display_width = 1200
# in pixels

map_size = 1000
# in pixels

map_rule_segments = 10
# number of colored segments to line the edge of the map with

map_rule_size = map_size // map_rule_segments
# length in pixels of each map rule segment

arm_scale = 25
# the "zoom factor" for our arms (less equals fewer arm "rings", but wider arms overall)
# recommended values are 10-100

galaxy_size = arm_scale * display_height
# internal measurement of galaxy size and scale

galaxy_height = 1000
# core height in light years (not used yet)

core_radius = galaxy_size / 10
# size of the core relative to the entire galaxy

xoff = int(map_size/2)
# half the display size in pixels

yoff = int(map_size/2)
# half the display size in pixels

mmxoff = 1010
#mini map x offset

mmyoff = 10
#mini map y offset

physical_galaxy_size = 100000
# in ly (milky way is 100,000 ly in diameter)

physical_galaxy_scale = physical_galaxy_size // map_size
# typically 100 ly / pixel

# colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
background = white