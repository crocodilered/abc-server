class Sign:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.profession = kwargs.get('profession')
        self.comments = kwargs.get('comments')
        self.created = kwargs.get('created')
        self.updated = kwargs.get('updated')
        self.secret_key = kwargs.get('secret_key')
        self.published = kwargs.get('published')
        self.serial = kwargs.get('serial')

    @staticmethod
    def from_row(row):
        if (
            type(row) is not tuple or
            len(row) != 10
        ):
            raise ValueError('Row must have 10 elements.')

        return Sign(
            id=row[0],
            name=row[1],
            email=row[2],
            profession=row[3],
            comments=row[4],
            created=row[5],
            updated=row[6],
            secret_key=row[7],
            published=row[8],
            serial=row[9],
        )

    def serialize(self):
        """ Coz of hi-load serialize object to tuple """
        return (
            self.name,
            self.profession,
            self.comments,
            round(self.published.timestamp()),
            self.serial,
        )
