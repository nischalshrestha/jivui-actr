(function() {
  var ReplayConcentrationGame = new JIVUI.UIModule();

  function Tile(letter, row, col){
    this.letter = letter;
    this.row = row;
    this.col = col;
  };

  var Board = { 
    level: 0,
    move: 0,
    firstTile: null,
    secondTile: null,
    click: 0,
    init: function(level) {
      this.level = level;
      this.reset();
    },
    reset: function() {
      this.move =  0;
      this.firstTile = null;
      this.secondTile = null;
      $(".cell").removeClass("revealed");
      $(".cell").removeClass("matched");
      $(".cell").removeClass("removed");
      $(".cell").html("");
      for(var i = 0; i < 4; i++) {
        for(var j = 0; j < 4; j++){
          $(".row" + i ).find(".col" + j).html(tiles[i][j]);
        }
      }
    },
    setFirstTile: function(tile){
      this.firstTile = tile;
    },
    setSecondTile: function(tile){
      this.secondTile = tile;
    },
    removeTiles: function(tile){
      // setTimeout(function(){
        $(".row" + this.firstTile.row).find(".col" + this.firstTile.col).removeClass("matched");
        $(".row" + this.secondTile.row).find(".col" + this.secondTile.col).removeClass("matched");
        // $(".row" + row).find(".col" + col).html("");
        // $(".row" + prevRow).find(".col" + prevCol).html("");
        // Make letters grey
        $(".row" + this.firstTile.row).find(".col" + this.firstTile.col).addClass("removed");
        $(".row" + this.secondTile.row).find(".col" + this.secondTile.col).addClass("removed");
      // }, 250);
    },
    revealTile: function(tile){
      $(".row" + tile.row).find(".col" + tile.col).addClass("revealed");
    },
    hideTiles: function(tile){
      // console.log("hiding tiles "+counter );
       // setTimeout(function(){
        $(".row" + this.firstTile.row).find(".col" + this.firstTile.col).removeClass("revealed");
        $(".row" + this.secondTile.row).find(".col" + this.secondTile.col).removeClass("revealed");
      // }, 1000);
    },
    isMatch: function(){
      if(this.firstTile.letter == this.secondTile.letter && (this.firstTile.row != this.secondTile.row || this.firstTile.col != this.secondTile.col)){
        $(".row" + this.firstTile.row).find(".col" + this.firstTile.col).addClass("matched");
        $(".row" + this.secondTile.row).find(".col" + this.secondTile.col).addClass("matched");
        return true;
      }
      return false;
    },
    setClick: function(time){
      this.click = time;
    },
    processClick: function(click) {
        this.move++;
        var target = click['target'];
        var row = click['row']-1;
        var col = click['col']-1;
        var tile = new Tile(target, row, col);
        // console.log("Clicked: "+" Row: "+row+" Col: "+col+" move: "+this.move);
        this.revealTile(tile);
        if(this.move % 2 == 0){
          this.move = 0;
          this.setSecondTile(tile);
          if(this.isMatch()){
            // console.log(target + " matches " + this.previous);
            this.removeTiles();
          } 
        } else {
          this.setFirstTile(tile);
        }
    }
  };

  var tiles = [
    ['C', 'A', 'C', 'P'],
    ['H', 'Q', 'I', 'E'],
    ['A', 'B', 'I', 'B'],
    ['H', 'Q', 'E', 'P']
  ];

  var counter = 0;

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
    counter = 0;
    clickBegin = 0;
  };

  ReplayConcentrationGame.onStop = function() {
    // console.log("pauses: "+pauses+" end: "+clickEnd);
    ReplayConcentrationGame.reset();
  };

  var clickBegin = 0;
  var pauses = 0;

  ReplayConcentrationGame.onFrame = function(frame, entry) {
    if(entry) {
      clickEnd = frame;
      if(clickBegin != 0){
        var difference = frame - clickBegin;
        if(difference >= 1000){
          pauses++;
          Board.hideTiles();
          // console.log("difference: "+difference);
        }
      }
      if(entry['click']){
        Board.processClick(entry['click']);
        if(counter++ == 0){
          clickBegin = frame;
          console.log("clickBegin: "+frame);
        } else {
          console.log("clickEnd: "+frame);
          counter = 0;
        }
      }
    }
  };

  JIVUI.registerUIModule(ReplayConcentrationGame);
})();
