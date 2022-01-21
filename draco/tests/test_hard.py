from draco import get_violations, is_satisfiable


def test_text_mark_without_text_channel():

    assert (
        get_violations(
            """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,text).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    """
        )
        == ["encoding_no_field_and_not_count", "text_mark_without_text_channel"]
    )

    assert (
        get_violations(
            """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,channel),e3,text).
    """
        )
        == ["encoding_no_field_and_not_count", "text_mark_without_text_channel"]
    )


def test_text_channel_without_text_mark():

    assert (
        get_violations(
            """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    attribute((mark,type),m1,bar).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    """
        )
        == ["encoding_no_field_and_not_count", "text_channel_without_text_mark"]
    )


def test_bin_and_aggregate():

    assert (
        get_violations(
            """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    entity(encoding,root,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,aggregate),e2,count).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    attribute((encoding,aggregate),e1,count).
    """
        )
        == ["bin_and_aggregate"]
    )


def test_no_encodings():

    assert (
        get_violations(
            """
    entity(mark,root,1).
    entity(encoding,1,2).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(mark,root,3).
    """
        )
        == ["encoding_no_field_and_not_count", "no_encodings"]
    )


def test_repeat_channel():

    assert is_satisfiable(
        """
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,y).
    """
    )

    assert (
        get_violations(
            """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(scale,root,3).
    attribute((scale,channel),3,x).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    entity(mark,root,1).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    entity(mark,root,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    """
        )
        == ["encoding_no_field_and_not_count", "repeat_channel"]
    )


def test_encoding_no_field_and_not_count():

    assert (
        get_violations(
            """
    entity(encoding,root,1).
    attribute((encoding,field),1,temp).
    attribute((encoding,aggregate),1,mean).
    """
        )
        == ["existing_field"]
    )

    assert is_satisfiable(
        """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    """
    )

    assert (
        get_violations(
            """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,mean).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )


def test_count_with_field():

    assert is_satisfiable(
        """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    """
    )

    assert (
        get_violations(
            """
    attribute((encoding,aggregate),1,count).
    attribute((encoding,field),1,temp).
    """
        )
        == ["count_with_field", "existing_field"]
    )


def test_point_tick_bar_without_x_or_y():

    assert (
        get_violations(
            """
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,color).
    """
        )
        == ["point_tick_bar_without_x_or_y", "encoding_no_field_and_not_count"]
    )

    assert (
        get_violations(
            """
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    """
        )
        == ["no_encodings"]
    )
