/**
 * Load the locations dropdown using the field with given selector.
 *
 * The dropdown is created using library called `select2`. The content of the
 * dropdown is loaded automtically as the values of the field changes.
 *
 * @param {string} fieldSelector The selector for the dropdown field to use. 
 * @param {string} apiKey The Weather API to use for the requests.
 */
function loadLocationsDropdown(fieldSelector, apiKey, initSelection = null) {
  $(fieldSelector).select2({
    theme: 'bootstrap-5',
    placeholder: 'Start typing...',
    minimumInputLength: 3,
    minimumResultsForSearch: 3,
    width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
    sorter: data => data.sort(function (a, b) { return a.text.localeCompare(b.text); }),
    ajax: {
      url: 'http://api.openweathermap.org/geo/1.0/direct',
      data: params => {
        return {
          q: params.term.trim(),
          limit: 5,
          appid: apiKey,
        }
      },
      dataType: 'json',
      delay: 300,
      cache: true,
      processResults: data => {
        results = data.map(item => {
          let text = item.name;
          if (item.state) { text = `${text}, ${item.state}`; }
          if (item.country) { text = `${text}, ${item.country}`; }
          return { id: `${item.lat}::${item.lon}::${text}`, text: text };
        });
        return { results };
      }
    }
  });

  if (initSelection) {
    const field = $(fieldSelector);
    const location = JSON.parse(initSelection);
    field.append(
      new Option(location.label, `${location.lat}::${location.lon}::${location.label}`, true, true)
    )
    field.trigger({ type: 'select2:select' });
  }
};