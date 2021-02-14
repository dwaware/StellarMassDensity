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
# the "zoom factor" for arms (less equals fewer arm "rings", but wider arms overall)
# recommended values are 1-100
# milky way looks good at 25

winding_factor = 1
# is the galaxy a ring (0) or a typical spiral (1)
# values between 0 and 1 will adjust how tightly wound the spirals are
# milky way looks good at 1

galaxy_size = arm_scale * display_height
# internal measurement of galaxy size as a function of scale

core_radius_percent = 10
# what's the relative size (%) of the galactic core
# recommended values are 0 to 50
# milky way looks good at 10

density_scale_factor_arms = 80
# density values can be arbitrary

density_scale_factor_core_outer = 5000

density_scale_factor_core_inner = 10000

physical_galaxy_size = 100000
# in ly
# milky is 100,000 ly in diameter

galaxy_height = 1000
# core height in light years (not used yet)

physical_galaxy_scale = physical_galaxy_size // map_size
# typically 100 ly / pixel

core_radius = core_radius_percent * galaxy_size / 100
# size of the core relative to the entire galaxy

xoff = int(map_size/2)
# half the display size in pixels

yoff = int(map_size/2)
# half the display size in pixels

mmxoff = 1010
#mini map x offset

mmyoff = 10
#mini map y offset

# colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
background = white