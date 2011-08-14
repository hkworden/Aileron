function main() {
  $(".chzn-select").chosen();
  $(".chzn-select").chosen().change(function() {
    $(".chzn-select option:selected").each(function() {
      window.location.href=$(this).attr('data-link');
    });
  });
}
