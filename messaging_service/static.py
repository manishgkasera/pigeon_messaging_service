
MESSAGE_STATUS = (
    (0, 'queued'),
    (1, 'sent'),
    (2, 'delivered'),
    (3, 'errored')
)
MESSAGE_STATUS_DICT = dict((v, k) for k, v in MESSAGE_STATUS)