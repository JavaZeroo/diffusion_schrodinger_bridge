import torch
import hydra
import os,sys
import matplotlib.pyplot as plt


sys.path.append('..')


from bridge.runners.ipf import IPFPredict


# SETTING PARAMETERS

@hydra.main(config_path="./conf", config_name="config_pred")
def main(args):
    args.device = 'cpu'
    print('Directory: ' + os.getcwd())
    # print(args)
    # args.device = 'cpu'

    ipf = IPFPredict(args)
    x = torch.randn(1, 1, 28, 28)
    pred = ipf.predict(x)
    print(pred)
    _, axes = plt.subplots(1, 2)

    # 在第一个子图中显示image1
    axes[0].imshow(x.squeeze(), cmap='gray')
    axes[0].axis('off')

    # 在第二个子图中显示image2
    axes[1].imshow(pred.squeeze(), cmap='gray')
    axes[1].axis('off')
    # 调整子图之间的间距
    plt.subplots_adjust(wspace=0.2)

    # 展示并排显示的图片
    plt.show()
    
if __name__ == '__main__':
    main()