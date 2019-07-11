def convert(x, convert_function, expected_type):
    """Convenience function to convert data types.

    Parameters
    ----------
    x :
        Input data to be converted.
    convert_function : function
        Function to apply to `x`.
    expected_type :
        Expected type of output data.

    Returns
    -------
        Converted data if convert successfully.

    Raise
    -------
        ValueError: Cannot convert input data to expected data type.
    """
    try:
        return convert_function(x)
    except ValueError as e:
        raise ValueError("Cannot convert input data of type {} to "
                         "{}: {}".format(type(x), expected_type, e))
