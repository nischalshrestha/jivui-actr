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
      // Remove the match style
      if(feedback){
        $(".row" + this.firstTile.row).find(".col" + this.firstTile.col).removeClass("matched");
        $(".row" + this.secondTile.row).find(".col" + this.secondTile.col).removeClass("matched");
      }
      // Make letters grey
      $(".row" + this.firstTile.row).find(".col" + this.firstTile.col).addClass("removed");
      $(".row" + this.secondTile.row).find(".col" + this.secondTile.col).addClass("removed");
    },
    revealTile: function(tile){
      $(".row" + tile.row).find(".col" + tile.col).addClass("revealed");
    },
    hideTiles: function(){
      // console.log("hiding 1st tile "+JSON.stringify(this.firstTile));
      // console.log("hiding 2nd tile "+JSON.stringify(this.secondTile));
      $(".row" + this.firstTile.row).find(".col" + this.firstTile.col).removeClass("revealed");
      $(".row" + this.secondTile.row).find(".col" + this.secondTile.col).removeClass("revealed");
    },
    isMatch: function(){
      if(this.firstTile.letter == this.secondTile.letter && (this.firstTile.row != this.secondTile.row || this.firstTile.col != this.secondTile.col)){
        if(feedback){
          $(".row" + this.firstTile.row).find(".col" + this.firstTile.col).addClass("matched");
          $(".row" + this.secondTile.row).find(".col" + this.secondTile.col).addClass("matched"); 
        }
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
        // console.log("Clicked: "+target+" Row: "+row+" Col: "+col+" move: "+this.move);
        this.revealTile(tile);
        if(this.move % 2 == 0){
          this.move = 0;
          this.setSecondTile(tile);
          if(this.isMatch()){
            match = true;
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
  var clickBegin = 0;
  var match = false;
  var hid = true;
  var feedback = true; // Make true to display match tile feedback

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
    match = false;
    hid = true;
  };

  ReplayConcentrationGame.onPlay = function() {
    ReplayConcentrationGame.reset();
  }

  ReplayConcentrationGame.onStop = function() {
    ReplayConcentrationGame.reset();
  };

  ReplayConcentrationGame.onFrame = function(frame, entry) {
    if(entry) {
      // If it has been 1s since tiles were displayed hide them
      if(clickBegin != 0){
        var difference = frame - clickBegin;
        if(difference >= 1000 && !hid){
          hid = true;
          Board.hideTiles();
        }
      }
      if(entry['click']){
        // If the previous tiles were not hidden already hide them
        if(clickBegin != 0 && counter == 0 && !hid){
          hid = true;
          Board.hideTiles();
        }
        if(match){
          Board.removeTiles();
          match = false; 
        }
        Board.processClick(entry['click']);
        if(counter++ == 0){
          clickBegin = frame;
        } else {
          counter = 0;
          hid = false;
        }
      }
    }
  };

  JIVUI.registerUIModule(ReplayConcentrationGame);
})();
