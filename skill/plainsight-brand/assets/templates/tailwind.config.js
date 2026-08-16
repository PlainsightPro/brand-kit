// Plainsight Tailwind config — drop into tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        ps: {
          blue:    '#000075',
          orange:  '#d5693a',
          cream:   '#fcf8f3',
          mist:    '#f6f6fa',
          'blue-55': 'rgba(0, 0, 117, 0.55)',
          'blue-18': 'rgba(0, 0, 117, 0.18)',
          'blue-08': 'rgba(0, 0, 117, 0.08)',
        },
      },
      fontFamily: {
        head: ['"Titillium Web"', '"Segoe UI"', 'Arial', 'sans-serif'],
        body: ['"Inter"', '"Segoe UI"', 'Arial', 'sans-serif'],
      },
    },
  },
};
