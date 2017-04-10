(function() {
  var ReplayConcentrationGame = new JIVUI.UIModule();

  var Board = { 
    level: 0,
    move: 0,
    previous: "",
    previousRow: 0,
    previousCol: 0,
    init: function(level) {
      this.level = level;
      this.reset();
    },
    reset: function() {
      this.move =  0;
      this.previous = "";
      this.previousRow = 0;
      this.previousCol = 0;
      $(".cell").removeClass("revealed");
      $(".cell").html("");
      for(var i = 0; i < 4; i++) {
        for(var j = 0; j < 4; j++){
          $(".row" + i ).find(".col" + j).html(tiles[i][j]);
        }
      }
    },
    setRow: function(row) {
      this.previousRow = row;
    },
    setCol: function(col) {
      this.previousCol = col;
    },
    setPreviousTile: function(tile){
      this.previous = tile;
      
    },
    removeTile: function(row, col){
      prevRow = this.previousRow;
      prevCol = this.previousCol;
      setTimeout(function(){
        $(".row" + row).find(".col" + col).html("");
        $(".row" + prevRow).find(".col" + prevCol).html("");
        $(".row" + row).find(".col" + col).removeClass("matched");
        $(".row" + prevRow).find(".col" + prevCol).removeClass("matched");
      }, 250);
    },
    revealTile: function(row, col){
      $(".row" + row).find(".col" + col).addClass("revealed");
    },
    hideTile: function(row, col){
      prevRow = this.previousRow;
      prevCol = this.previousCol;
       setTimeout(function(){
        $(".row" + row).find(".col" + col).removeClass("revealed");
        $(".row" + prevRow).find(".col" + prevCol).removeClass("revealed");
      }, 1000);
    },
    isMatch: function(tile, row, col){
      if(tile == this.previous && (row != this.previousRow || col != this.previousCol)){
        $(".row" + row).find(".col" + col).addClass("matched");
        $(".row" + this.previousRow).find(".col" + this.previousCol).addClass("matched");
        return true;
      }
      return false;
    },
    processClick: function(click) {
        this.move++;
        var target = click['target'];
        var row = click['row']-1;
        var col = click['col']-1;
        // console.log("Clicked: "+" Row: "+row+" Col: "+col+" move: "+this.move);
        this.revealTile(row, col);
        if(this.move % 2 == 0){
          if(this.isMatch(target, row, col)){
            // console.log(target + " matches " + this.previous);
            this.removeTile(row, col);
          } else {
            this.hideTile(row, col);
          }
          this.move = 0;
        } else {
          this.setPreviousTile(target);
          this.setRow(row);
          this.setCol(col);
        }
    }
  };

  // C   A   C   P
  // H   Q   I   E
  // A   B   I   B
  // H   Q   E   P

  var tiles = [
    ['C', 'A', 'C', 'P'],
    ['H', 'Q', 'I', 'E'],
    ['A', 'B', 'I', 'B'],
    ['H', 'Q', 'E', 'P']
  ];

  ReplayConcentrationGame.init = function(state) {
      $('#dataTitle').html("Concentration");
  };

  ReplayConcentrationGame.onDataProcessed = function(settings, data) {
    $('#dataTitle').html(settings.title);
    Board.init(settings.level);
    ReplayConcentrationGame.reset();
  };

  ReplayConcentrationGame.reset = function() {
    Board.reset();
  };

  ReplayConcentrationGame.onStop = function() {
    ReplayConcentrationGame.reset();
  };

  ReplayConcentrationGame.onFrame = function(frame, entry) {
    if(entry && entry['click']) {
      Board.processClick(entry['click'])
    }
  };

  JIVUI.registerUIModule(ReplayConcentrationGame);
})();
