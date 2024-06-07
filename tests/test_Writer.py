from ml_instrumentation.Writer import Writer, Point

def test_write1():
    writer = Writer(
        db_path=':memory:',
        low_watermark=2,
        high_watermark=4,
    )

    d = Point(
        metric='measurement-1',
        exp_id=0,
        frame=0,
        data=1.1,
    )
    writer.write(d)

    # should get back a list of datapoints for this measurement
    points = writer.read_metric('measurement-1')
    assert points == [
        (0, 0, 1.1),
    ]

    d = Point(
        metric='measurement-1',
        exp_id=0,
        frame=1,
        data=2.2
    )
    writer.write(d)

    points = writer.read_metric('measurement-1')
    assert points == [
        (0, 0, 1.1),
        (1, 0, 2.2),
    ]

    writer.close()

def test_write2():
    writer = Writer(
        db_path=':memory:',
        low_watermark=256,
        high_watermark=512,
    )

    for i in range(1_000):
        d = Point(
            metric='measurement-1',
            exp_id=0,
            frame=i,
            data=i * 1.1,
        )
        writer.write(d)

        if i % 3 == 0:
            d2 = d._replace(metric='measurement-2')
            writer.write(d2)

    points = writer.read_metric('measurement-1')
    assert len(points) == 1_000
    for i in range(1_000):
        assert points[i].frame == i
        assert points[i].measurement == i * 1.1

    points = writer.read_metric('measurement-2')
    assert len(points) == 334
