# Makefile for daughterboard-testing-bottom KiCad project

PROJECT_NAME := daughterboard-testing-bottom
PROJECT_DIR := $(shell pwd)
PROJECT_FILE := $(PROJECT_NAME).kicad_pro
SCHEMATIC_FILE := $(PROJECT_NAME).kicad_sch
PCB_FILE := $(PROJECT_NAME).kicad_pcb

OUTPUTS_DIR := outputs

# Get the short commit hash of the last commit that changed this folder
SHORT_HASH := $(shell git log -1 --format=%h -- . 2>/dev/null || echo "unknown")

.PHONY: all schematic-pdf gerbers aisler-upload clean update-commit-hash

all: schematic-pdf gerbers

# Update COMMIT_HASH text variable in project file
update-commit-hash:
	@echo "Updating COMMIT_HASH to $(SHORT_HASH)..."
	@jq --arg hash "$(SHORT_HASH)" '.text_variables.COMMIT_HASH = $$hash' $(PROJECT_FILE) > tmp.json && mv tmp.json $(PROJECT_FILE)

# Export schematic as PDF
schematic-pdf: update-commit-hash
	@mkdir -p $(OUTPUTS_DIR)
	@echo "Exporting schematic PDF..."
	kicad-cli sch export pdf \
		--output $(OUTPUTS_DIR)/$(PROJECT_NAME)-schematic.pdf \
		$(SCHEMATIC_FILE)
	@echo "Schematic PDF exported to $(OUTPUTS_DIR)/$(PROJECT_NAME)-schematic.pdf"

# Export Gerber files and drill files
gerbers: update-commit-hash
	@mkdir -p $(OUTPUTS_DIR)/gerbers
	@echo "Exporting Gerber files..."
	kicad-cli pcb export gerbers \
		--output $(OUTPUTS_DIR)/gerbers/ \
		--layers "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
		--subtract-soldermask \
		$(PCB_FILE)
	@echo "Exporting drill files..."
	kicad-cli pcb export drill \
		--output $(OUTPUTS_DIR)/gerbers/ \
		--format excellon \
		--excellon-units mm \
		$(PCB_FILE)
	@echo "Gerbers exported to $(OUTPUTS_DIR)/gerbers/"

# Prepare PCB file for Aisler upload (replace COMMIT_HASH variable with actual hash)
aisler-upload: update-commit-hash
	@mkdir -p $(OUTPUTS_DIR)/aisler
	@echo "Preparing PCB file for Aisler upload..."
	@echo "Replacing \$${COMMIT_HASH} with $(SHORT_HASH) in PCB file..."
	@sed 's/\$${COMMIT_HASH}/$(SHORT_HASH)/g' $(PCB_FILE) > $(OUTPUTS_DIR)/aisler/$(PROJECT_NAME).kicad_pcb
	@echo "Aisler-ready PCB file exported to $(OUTPUTS_DIR)/aisler/$(PROJECT_NAME).kicad_pcb"

clean:
	rm -rf $(OUTPUTS_DIR)

# Show current commit hash
info:
	@echo "Project: $(PROJECT_NAME)"
	@echo "Last commit hash for this folder: $(SHORT_HASH)"
