db.getCollection('api_request').aggregate(
  [
    {
      $lookup: {
        from: 'text_example',
        localField: 'generation_id',
        foreignField: 'generation_id',
        as: 'text_example'
      }
    },
    {
      $lookup: {
        from: 'ai_feedback',
        localField: 'generation_id',
        foreignField: 'generation_id',
        as: 'ai_feedback'
      }
    },
    { $sort: { timestamp: -1 } },
    { $unwind: '$ai_feedback' },
    {
      $project: {
        'text_example._id': 0,
        'ai_feedback._id': 0,
        _id: 0,
        'api_request.generation_id': 0,
        'text_example.generation_id': 0,
        generation_id: 0
      }
    }
  ],
  { maxTimeMS: 60000, allowDiskUse: true }
);