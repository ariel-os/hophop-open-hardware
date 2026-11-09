THICKNESS = 4;

module file() {
    import("pcb-with-usb-connector-turned-into-convex-hull.stl", convexity=3);
}

module slice(layer) {
    projection() {
        intersection() {
            file();
            translate([-1000, -1000, THICKNESS * layer]) cube([2000, 2000, THICKNESS]);
        }
    }
}

module slices() {
    // just the PCB
    translate([0, 0, 0]) slice(-0.9);
    translate([35, 0, 0]) slice(0);
    translate([70, 0, 0]) slice(1);
    translate([105, 0, 0]) slice(2);
}

slices();
translate([0, -100, 0])
offset(-1) offset(1) {
    slices();
}
