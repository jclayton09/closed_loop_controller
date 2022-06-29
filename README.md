# Config File
you can either set a limit or constant_variable

With the config there are main attribute that are needed for the program to run and then others depend on the plugins that are written for them
e.g. this config is including the main variables
Example Config:
```yaml 
input:
  data_format: Sql
  interval: 30s
  changing_variable: chiller2_litreperminute
  constant_variable: chiller1_litreperminute
output:
  output_format: http
  constant_variable_lower_limit: 2
  constant_variable_upper_limit: 10
  minimum_step: 0.5
```

And here is the same config with the added plugin variables

Example Config:
```yaml 
input:
  data_format: Sql
  interval: 30s
  changing_variable: chiller2_litreperminute
  constant_variable: chiller1_litreperminute
  database_connection: postgresql://telegraf:Yr;rhtsg@192.168.30.4/timescale
  table: josh_testing_1
output:
  output_format: http
  constant_variable_lower_limit: 2
  constant_variable_upper_limit: 10
  minimum_step: 0.5
  changing_url: 'http://127.0.0.1:8000/voltage/set/'
  current_url: 'http://127.0.0.1:8000/voltage/set'
```

# Plugins
For the plugins I have coded it so whatever is defined in the yaml input section of the config gets passed into the plugin

## Input
To write a plugin for the input all you need is a function called `message()` this just lets the user know that the plugin is loaded correctly
and then a function called `return_to_main()` which returns a dictionary like bellow
``
{'changing_variable': value, 'constant_variable': value}
``
You can use code any functions in the world to help support the code however the main program will only read these `message()` &  `return_to_main()`
## Output
To write a plugin for the output it has just an extra function than the input.
- `def message():`
- `def output_from_main(value, **kwargs):`
- `def current_value(**kwargs):`

### message()
This is just a little print statment along the lines of `print(f"Output plugin loaded: http")`. This is just to let the user know that the plugin has been recognised and callable by the main program

### current_value()
This is a quick little function to interact with your system and provide the current setting so that the main code knows what value to change it too

### output_from_main()
This function is where the change value from the main program is passed to as well as the `**kwargs` which in this case is just taking the yaml outputs section and passing it through.