/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './brujula_profesional_digital/templates/**/*.{html,js}',
    './brujula_profesional_digital/components/**/*.{html,js}',
  ],
  theme: {
    extend: {
      spacing: {
        '128': '32rem',
        '154': '48rem',
        '256': '64rem',
        '128': '32rem',
      }
    },
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ]
}
