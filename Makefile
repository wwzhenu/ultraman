index: 
	# 安装paddlepaddle
	pip3 install paddlepaddle -i https://mirror.baidu.com/pypi/simple
	# 安装依赖
	pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
	# cd deploy && mkdir models
	cd deploy && cd models && wget https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/models/inference/ppyolov2_r50vd_dcn_mainbody_v1.0_infer.tar && tar -xf ppyolov2_r50vd_dcn_mainbody_v1.0_infer.tar 
	cd deploy && cd models && wget https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/models/inference/product_ResNet50_vd_aliproduct_v1.0_infer.tar && tar -xf product_ResNet50_vd_aliproduct_v1.0_infer.tar 
	cd deploy && cd models && wget https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/models/inference/cartoon_rec_ResNet50_iCartoon_v1.0_infer.tar && tar -xf cartoon_rec_ResNet50_iCartoon_v1.0_infer.tar
	# build vector
	cd deploy && cd vector_search && make