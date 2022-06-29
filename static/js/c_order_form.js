function re_fresh(Rng, Lbl) {
  var slider = document.getElementById(Rng);
  var output = document.getElementById(Lbl);
  output.innerHTML = slider.value;
  slider.oninput = function() {
    output.innerHTML = this.value;
  };
}
