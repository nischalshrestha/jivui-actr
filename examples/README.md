# JIVUI Example

Here is an example of using JIVUI to visualize ACT-R model data.

### Citation

The example data is produced from the speed version the model. For more detail see the below paper on the context for the study and in particular section 3.1.

Domínguez, I. X., Goodwin, P. R., Roberts, D. L., & St. Amant, R. (2017). Human subtlety proofs: Using computer games to model cognitive processes for cybersecurity. International Journal of Human-Computer Interaction, 33(1), 44-54. doi:10.1080/10447318.2016.1232229

---

## Concentration Game - Speed Round

This example visualizes one round of a computer-based Concentration game played by an ACT-R model for the speed condition.

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
  * ReplayConcentrationGame (see gameplay.js)
