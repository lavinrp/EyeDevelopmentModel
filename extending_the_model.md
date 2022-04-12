# Extending The Model
EDM was designed to be extended. Users are encouraged to extend, improve,
or otherwise edit any part of the software necessary to test out new hypotheses or even to just
explore. While any part of the simulation CAN be modified we have provided the `quick_change`
module for tweaking the simulation without significantly modifying the core of the model.

# quick_change module
`quick_change` contains everything necessary to add new stages of development to the simulation, 
remove / modify existing ones, alter the behavior of cells, or change the way that cells
are displayed.

## CellDisplayRules
These rules govern the way that the epithelium is displayed. They are found in `CellDisplayRules.py`
### `determine_cell_color`
Determines the color of a cell. Return values in RGB format
### `determine_cell_fill`
Determines if cells are displayed as filled circles or just circle outlines

## CellEvents
These are callable objects that are invoked on a cell once per simulation tick.
Cell events can be added to a cell via the public `cell_events` list property on `Cell`.

Existing cell events are located in `CellEvents.py`. The default events that cells begin with
are specified in `Epithelium.create_cell_sheet` in the `epithelium_backend` module.

Cell events are usually added to cells by a `FurrowEvent`.

## FurrowEventList
The `furrow_event_list` contains the set of events that will act on the epithelium as the
furrow advances. It is located in `FurrowEventList.py`

The `furrow_event_list` is a list of `FurrowEvent` objects. Each furrow event object has a 
name, a distance from the furrow, a set of parameters (called `field_types`) and a function that
is invoked every simulation tick on the small slice of the epithelium that is the correct
distance from the furrow line.

Every `FurrowEvent` in the `furrow_event_list` is displayed in the **simulation overview** tab
of the simulation. A settings entry with the name of the event, distance from the furrow,
and all parameters will be auto generated. When the simulation runs The parameters will have
the user input values. Only numeric parameters are supported at this time.

The function invoked by a `FurrowEvent` must take three parameters. 
1. `field_types` (a dictionary of `str` to `FieldType` object). These are the user provides inputs to the event.
2. `epethelium` The full epithelium currently being simulated
3. `cells` The slice of cells that the `FurrowEvent` is currently operating on.

See the existing functions and `FurrowEvent` instances in `FurrowEventList.py` for examples.