pcb.stl: ../hardware/hophop-development-board.kicad_pcb
	kicad-cli pcb export stl --subst-models --drill-origin -f -o $@ $<

pcb-with-usb-connector-turned-into-convex-hull.stl: pcb.stl
	# created by selecting something on the USB connector, selecting
	# everything connected, moving that into a separate layer, turning it into
	# a convex hull, flattening it back, and then selecting everything that is
	# a non-manifold edge, all connected faces, and deleting that.
	echo "manual process; follow instructions in the comment"
	exit 1

extracted.svg: extract.scad pcb-with-usb-connector-turned-into-convex-hull.stl
	openscad $< -o $@
