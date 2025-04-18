#【3】 固化保存模型
import paddle
import paddle.fluid as fluid
import codecs

init_train_parameters()


def freeze_model():
    exe = fluid.Executor(fluid.CPUPlace())

    ues_tiny = train_params['use_tiny']
    yolo_config = train_params['yolo_tiny_cfg'] if ues_tiny else train_params['yolo_cfg']
    path = train_params['save_model_dir']

    model = get_yolo(ues_tiny, train_params['class_dim'],
                     yolo_config['anchors'], yolo_config['anchor_mask'])
    image = fluid.layers.data(name='image', shape=yolo_config['input_size'], dtype='float32')
    image_shape = fluid.layers.data(name="image_shape", shape=[2], dtype='int32')

    boxes = []
    scores = []
    outputs = model.net(image)
    downsample_ratio = model.get_downsample_ratio()

    for i, out in enumerate(outputs):
        box, score = fluid.layers.yolo_box(x=out,
                                           img_size=image_shape,
                                           anchors=model.get_yolo_anchors()[i],
                                           class_num=model.get_class_num(),
                                           conf_thresh=train_params['valid_thresh'],
                                           downsample_ratio=downsample_ratio,
                                           name="yolo_box_" + str(i))
        boxes.append(box)
        scores.append(fluid.layers.transpose(score, perm=[0, 2, 1]))
        downsample_ratio //= 2

    pred = fluid.layers.multiclass_nms(bboxes=fluid.layers.concat(boxes, axis=1),
                                       scores=fluid.layers.concat(scores, axis=2),
                                       score_threshold=train_params['valid_thresh'],
                                       nms_top_k=train_params['nms_top_k'],
                                       keep_top_k=train_params['nms_pos_k'],
                                       nms_threshold=train_params['nms_thresh'],
                                       background_label=-1,
                                       name="multiclass_nms")

    freeze_program = fluid.default_main_program()

    fluid.io.load_persistables(exe, path, freeze_program)
    freeze_program = freeze_program.clone(for_test=True)
    print("freeze out: {0}, pred layout: {1}".format(train_params['freeze_dir'], pred))
    # 保存模型
    fluid.io.save_inference_model(train_params['freeze_dir'],
                                  ['image', 'image_shape'],
                                  pred, exe, freeze_program)
    print("freeze end")


if __name__ == '__main__':
    freeze_model()