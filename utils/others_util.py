def convert(x, convert_function, expected_type, force=False):
    """Convenience function to convert data types.

    Parameters
    ----------
    x :
        Input data to be converted.
    convert_function : function
        Function to apply to `x`.
    expected_type :
        Expected type of output data.
    force: boolean
        By default, if input data type matches expected type, there will be no
        further transformation. Use `force=True` to force using `convert_function`.

    Returns
    -------
        Converted data if convert successfully.

    Raise
    -------
        ValueError: Cannot convert input data to expected data type.
    """
    if (not isinstance(x, expected_type)) or force:
        try:
            return convert_function(x)
        except ValueError as e:
            raise ValueError("Cannot convert input data of type {} to "
                             "{}: {}".format(type(x), expected_type, e))
    else:
        return x
