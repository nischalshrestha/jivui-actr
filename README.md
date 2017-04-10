# JIVUI Example

This is an example of using JIVUI to visualize ACT-R model data.

### Citation

The example data was produced from the speed version of the model. Refer to the paper below for the context of the study, particularly section 3.1 which discusses the game and the models in more detail.

Domínguez, I. X., Goodwin, P. R., Roberts, D. L., & St. Amant, R. (2017). Human subtlety proofs: Using computer games to model cognitive processes for cybersecurity. International Journal of Human-Computer Interaction, 33(1), 44-54. doi:10.1080/10447318.2016.1232229

---

## Concentration Game - Speed Round

This example visualizes one round of a computer-based Concentration game played by an ACT-R model.

### Library Dependencies
  * jQuery
  * jQueryUI
  * FontAwesome
  * Bootstrap 3

### Plugins Used

#### Preprocessors
  * Gaze fixations (used to simulate the cursor movements in ACT-R; see parser.py)

#### UI Modules
  * File Loader
  * Controls
  * Timeline
  * Custom replay area
  * ReplayConcentrationGame (custom UI Module; see gameplay.js)
