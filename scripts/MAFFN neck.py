import gen_layer
import math


num_trans_layers = 3
num_dense_layers = 5
num_class = 5 
use_pooling = True
use_aux_loss = False

def gen_data_layer(f, label_source=label_source, data_source=data_source,
                   local_dict=local_dict_source,train_batch_size=64,
                   test_batch_size=80, channel=1, train_num_words=200,
                   test_num_words=100, crop_height=100, crop_width=300):
    f.write(gen_layer.generate_data_layer_str(
        label_source, data_source, local_dict,train_batch_size, test_batch_size,
        channel, train_num_words, test_num_words,crop_height, crop_width))

def gen_trans_layer(f, num_layers=num_trans_layers, num_output=64, kernel_h=1,
                    kernel_w=1, pad_h=0, pad_w=0):
    #generate (conv+bn+relu)*num_layers
    f.write('#----Transform Feature Dimension----\n')
    for i in range(num_layers):
        if i == 0:
            f.write(gen_layer.generate_conv_layer_str(
                'trans_layer_conv'+str(i), 'data', 'trans_layer_conv'+str(i), num_output, 1, 300, 0, 0))
        else:
            f.write(gen_layer.generate_conv_layer_str(
                'trans_layer_conv'+str(i), 'trans_layer_bn'+str(i-1), 'trans_layer_conv'+str(i),
                num_output, kernel_h, kernel_w, pad_h, pad_w))

        f.write(gen_layer.generate_bn_layer_str(
            'trans_layer_bn'+str(i), 'trans_layer_conv'+str(i), 'trans_layer_bn'+str(i)))
        f.write(gen_layer.generate_activation_layer_str(
            'trans_layer_relu'+str(i), 'trans_layer_bn'+str(i)))

def gen_dense_layer(f, num_layers=num_dense_layers, num_output=64, kernel_h=3,
                    kernel_w=1, pad_h=1, pad_w=0, use_pooling=use_pooling):
    #generate (conv+concat+bn+relu)*num_layers
    f.write('#----Dense CNN----\n')
    for i in range(num_layers):
        if i == 0:
            #conv
            f.write(gen_layer.generate_conv_layer_str(
                'dense_layer_conv'+str(i), 'trans_layer_bn'+str(num_trans_layers-1), 'dense_layer_conv'+str(i),
                num_output, kernel_h, kernel_w, pad_h, pad_w))

            #concat
            bottom_list = ['dense_layer_conv0']
            for j in range(num_trans_layers):
                bottom_list.append('trans_layer_conv'+str(j))
            f.write(gen_layer.generate_concat_layer_str('dense_layer_concat'+str(i), bottom_list,
                                                      'dense_layer_concat'+str(i)))
        else:
            #conv
            if use_pooling:
                f.write(gen_layer.generate_conv_layer_str(
                    'dense_layer_conv'+str(i), 'dense_layer_pool'+str(i-1), 'dense_layer_conv'+str(i),
                    num_output, kernel_h, kernel_w, pad_h, pad_w))
            else:
                f.write(gen_layer.generate_conv_layer_str(
                    'dense_layer_conv'+str(i), 'dense_layer_bn'+str(i-1), 'dense_layer_conv'+str(i),
                    num_output, kernel_h, kernel_w, pad_h, pad_w))

            #concat
            if use_pooling:
                bottom_list = ['dense_layer_conv'+str(i), 'dense_layer_pool'+str(i-1)]
                f.write(gen_layer.generate_concat_layer_str('dense_layer_concat'+str(i), bottom_list,
                                                      'dense_layer_concat'+str(i)))
            else:
                bottom_list = ['dense_layer_conv'+str(i), 'dense_layer_bn'+str(i-1)]
                f.write(gen_layer.generate_concat_layer_str('dense_layer_concat'+str(i), bottom_list,
                                                      'dense_layer_concat'+str(i)))
        #bn
        f.write(gen_layer.generate_bn_layer_str(
            'dense_layer_bn'+str(i), 'dense_layer_concat'+str(i), 'dense_layer_bn'+str(i)))
        #relu
        f.write(gen_layer.generate_activation_layer_str(
            'dense_layer_relu'+str(i), 'dense_layer_bn'+str(i)))
        #pooling
        if use_pooling and i < num_layers-1:
            f.write(gen_layer.generate_pooling_layer_str(
                'dense_layer_pool'+str(i), 'dense_layer_bn'+str(i), 'dense_layer_pool'+str(i)))

#Multi-scale Attention Feature Fusion Network#
-----------------------------------------------
def attention_layer(m, n=2, out=64,h_kernel=1, h_pad=0, w_kernel=1, w_pad=0):
def h_pooled(x):
for i in range (dense_layers - 1):
x = math.ceil(0.5*(x - 1)) +1
return int(x)
height = calc_pooled_height(100)
group = trans_layers + dense_layers
for i in range(layers):
#conv
if i == 0:
        f.write(layer.generate_conv_layer_str('attention_layer_conv'+str(i),  
                      'dense_layer_bn'+str(dense_layers-1), 'attention_layer_conv'+str(i),
                       output*group, h_kernel, w_kernel, h_pad, w_pad, group))
else:
        f.write(gen_layer.generate_conv_layer_str(
             'attention_layer_conv'+str(i), 'attention_layer_bn'+str(i-1), 
             'attention_layer_conv'+str(i),
              output*group, h_kernel, w_kernel, h_pad, w_pad, group))
        f.write(gen_layer.generate_bn_layer_str('attention_layer_bn'+str(i), 
            'attention_layer_conv'+str(i), 'attention_layer_bn'+str(i)))
        f.write(gen_layer.generate_activation_layer_str('attention_layer_relu'+str(i), 
           'attention_layer_bn'+str(i)))
        #bn
        f.write(gen_layer.generate_bn_layer_str(
            'attention_layer_bn'+str(i), 'attention_layer_conv'+str(i), 'attention_layer_bn'+str(i)))
        #relu
        f.write(gen_layer.generate_activation_layer_str(
            'attention_layer_relu'+str(i), 'attention_layer_bn'+str(i)))

    #filter ensemble
    f.write(gen_layer.generate_slice_layer_str('attention_scale_slice', 'attention_layer_bn'+str(num_layers-1),
                                               'attention_scale', num_group, num_output))
    for i in range(num_group):
        f.write(gen_layer.generate_permute_layer_str('attention_permute'+str(i), 'attention_scale'+str(i),
                                               'attention_permute'+str(i), [0, 3, 2, 1]))
        f.write(gen_layer.generate_reduction_layer_str('attention_reduction'+str(i), 'attention_permute'+str(i),
                                               'attention_reduction'+str(i), 3))
    bottom_list = []
    for i in range(num_group):
        bottom_list.append('attention_reduction'+str(i))
    f.write(gen_layer.generate_concat_layer_str('attention_scale_concat', bottom_list, 'attention_scale_concat'))

    #scale reweight
    f.write(gen_layer.generate_slice_layer_str('attention_height_slice', 'attention_scale_concat',
                                               'attention_height', num_height, 1, 2))
    for i in range(num_height):
        f.write(gen_layer.generate_fc_layer_str('attention_height_fc1_'+str(i), 'attention_height'+str(i),
                                               'attention_height_fc1_'+str(i), 64))
        f.write(gen_layer.generate_fc_layer_str('attention_height_fc2_'+str(i), 'attention_height_fc1_'+str(i),
                                               'attention_height_fc2_'+str(i), 32))
        f.write(gen_layer.generate_fc_layer_str('attention_height_fc3_'+str(i), 'attention_height_fc2_'+str(i),
                                               'attention_height_fc3_'+str(i), num_group))
        f.write(gen_layer.generate_reshape_layer_str('attention_height_reshape'+str(i), 'attention_height_fc3_'+str(i),
                                               'attention_height_reshape'+str(i), [0, 0, 1, 1]))
    bottom_list = []
    for i in range(num_height):
        bottom_list.append('attention_height_reshape'+str(i))
    f.write(gen_layer.generate_concat_layer_str('attention_height_concat', bottom_list, 'attention_height_concat', 2))
    f.write(gen_layer.generate_softmax_layer_str('attention_weight', 'attention_height_concat', 'attention_weight'))
    f.write(gen_layer.generate_slice_layer_str('attention_weight_slice', 'attention_weight',
                                               'attention_weight_slice', num_group, 1))
    bottom_list = []
    for i in range(num_group):
        f.write(gen_layer.generate_tile_layer_str('attention_weight_tile'+str(i), 'attention_weight_slice'+str(i),
                                                  'attention_weight_tile'+str(i), 1, num_output))
        f.write(gen_layer.generate_eltwise_layer_str('attention_reweight'+str(i), ['attention_scale'+str(i), 'attention_weight_tile'+str(i)],
                                                  'attention_reweight'+str(i), 'PROD'))
        bottom_list.append('attention_reweight'+str(i))
    f.write(gen_layer.generate_eltwise_layer_str('attention_reweight_sum', bottom_list, 'attention_reweight_sum', 'SUM'))

def gen_classification_layer(f, num_output=64, num_class=num_class, dropout_ratio=0.7):
    f.write(gen_layer.generate_flatten_layer_str('attention_reweight_flatten', 'attention_reweight_sum', 'attention_reweight_flatten'))
    f.write(gen_layer.generate_dropout_layer_str('attention_reweight_dropout', 'attention_reweight_flatten', 'attention_reweight_dropout', dropout_ratio))
    f.write(gen_layer.generate_fc_layer_str('classification_fc1', 'attention_reweight_dropout', 'classification_fc1', num_output))
    f.write(gen_layer.generate_dropout_layer_str('classification_dropout', 'classification_fc1', 'classification_dropout', dropout_ratio))
    f.write(gen_layer.generate_fc_layer_str('classification_fc2', 'classification_dropout', 'classification_fc2', num_class, [10, 2, 10, 2]))
    f.write(gen_layer.generate_softmax_loss_str('classification_loss', 'classification_fc2', 'label', 'classification_loss'))
    f.write(gen_layer.generate_accuracy_str('classification_accuracy', 'classification_fc2', 'label', 'classification_accuracy'))
    if use_aux_loss:
        num_group = num_trans_layers + num_dense_layers
        for i in range(num_group):
            f.write(gen_layer.generate_pooling_layer_str(
                'attention_pool_scale'+str(i), 'attention_scale'+str(i), 'attention_pool_scale'+str(i), 'global_pooling'))
            f.write(gen_layer.generate_flatten_layer_str('attention_flatten_scale'+str(i), 'attention_pool_scale'+str(i),
                                                         'attention_flatten_scale'+str(i)))
            f.write(gen_layer.generate_dropout_layer_str('attention_dropout_scale'+str(i), 'attention_flatten_scale'+str(i),
                                                         'attention_dropout_scale'+str(i), dropout_ratio))
            f.write(gen_layer.generate_fc_layer_str('classification_fc1_scale'+str(i), 'attention_dropout_scale'+str(i),
                                                    'classification_fc1_scale'+str(i), num_output))
            f.write(gen_layer.generate_dropout_layer_str('classification_dropout_scale'+str(i), 'classification_fc1_scale'+str(i),
                                                         'classification_dropout_scale'+str(i), dropout_ratio))
            f.write(gen_layer.generate_fc_layer_str('clasification_fc2_scale'+str(i), 'classification_dropout_scale'+str(i),
                                                    'classification_fc2_scale'+str(i), num_class, [10, 2, 10, 2]))
            f.write(gen_layer.generate_softmax_loss_str('classification_loss_scale'+str(i), 'classification_fc2_scale'+str(i),
                                                        'label', 'classification_loss_scale'+str(i)))
            f.write(gen_layer.generate_accuracy_str('classification_accuracy_scale'+str(i), 'classification_fc2_scale'+str(i),
                                                    'label', 'classification_accuracy_scale'+str(i)))

def gen_net():
    with open('train_test_net.prototxt', 'w') as f:
        gen_data_layer(f)
        gen_trans_layer(f)
        gen_dense_layer(f)
        gen_attention_layer(f)
        gen_classification_layer(f)

if __name__ == '__main__':
    gen_net()


