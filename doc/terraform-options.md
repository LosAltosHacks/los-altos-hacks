# Thinking about TF

Two main options for staging/prod separation:

1. Divide by workspace
  - common elements factored out without module use
  - for things like, not having an RDS instance for staging, this means weird conditionals in the configuration

2. HAve two fully different configurations
  - factoring out modules is annoying
