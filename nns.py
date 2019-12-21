import argparse
import numpy as np

from utils import l2_dist
from embed_cnn import test_recall


def topk(xq, xb, xt, query_knn_, query_dist, train_knn_, train_dist):
    test_recall(xb, xq, query_knn_)


def linear_fit(x, y):
    weights = np.polyfit(x, y, deg=1)
    poly1d_fn = np.poly1d(weights)
    return poly1d_fn


def ann(xq, xb, xt, query_knn_, query_dist, train_knn_, train_dist):
    scales = [1, 2, 4, 8, 16, 32, 64]
    thresholds = [1, 5, 10, 15, 20, 25, 50, 75, 100, 125, 150]
    train_dist_l2 = l2_dist(xt, xt)
    query_dist_l2 = l2_dist(xq, xb)
    threshold2dist = linear_fit(train_dist, train_dist_l2)
    print(" threshold\t threshold_l2\t", end='')
    for scale in scales:
        print("%d \t" % scale, end='')
    for threshold in thresholds:
        gt = [np.argwhere(dist <= threshold) for dist in query_dist]
        threshold_l2 = threshold2dist(threshold)
        print("{}\t {}\t".format(threshold, threshold_l2), end=',\t ')
        for scale in scales:
            items = [np.argwhere(dist <= threshold_l2 * scale) for dist in query_dist_l2]
            recall = np.mean([len(np.intersect1d(i, j)) / len(i) for i, j in zip(gt, items)])
            print("%.4f \t" % recall, end='')
        print()


def load_vec():
    parser = argparse.ArgumentParser(description="HyperParameters for String Embedding")

    parser.add_argument("--dataset", type=str, default="word", help="dataset")
    parser.add_argument("--nt", type=int, default=1000, help="# of training samples")
    parser.add_argument("--nq", type=int, default=1000, help="# of query items")
    parser.add_argument("--shuffle-seed", type=int, default=808, help="seed for shuffle")

    parser.add_argument("--recall", action="store_true", default=False, help="print recall")
    parser.add_argument("--embed", type=str, default="cnn", help="embedding method")
    parser.add_argument("--maxl", type=int, default=0, help="max length of strings")
    args = parser.parse_args()
    data_file = "model/{}/{}/{}/nt{}_nq{}{}".format(
        args.shuffle_seed,
        args.embed,
        args.dataset,
        args.nt,
        args.nq,
        "" if args.maxl == 0 else "_maxl{}".format(args.maxl),
    )

    print("# loading embeddings")
    xb = np.load("{}/embedding_xb.npy".format(data_file))
    xt = np.load("{}/embedding_xt.npy".format(data_file))
    xq = np.load("{}/embedding_xq.npy".format(data_file))

    data_file = "model/{}/{}/{}/nt{}_nq{}{}".format(
        args.shuffle_seed,
        'cnn',
        args.dataset,
        args.nt,
        args.nq,
        "" if args.maxl == 0 else "_maxl{}".format(args.maxl),
    )
    print("# loading distances")
    train_dist = np.load(data_file + '/train_dist.npy')
    train_knn_ = np.load(data_file + '/train_knn.npy')
    query_dist = np.load(data_file + '/query_dist.npy')
    query_knn_ = np.load(data_file + '/query_knn.npy')
    if args.embed == 'gru':
        # TODO bugs to fix
        xq, xt = xt, xq

    xq = xq[:100, :]
    xb = xb[:100, :]
    ann(xq, xb, xt, query_knn_, query_dist, train_knn_, train_dist)
    topk(xq, xb, xt, query_knn_, query_dist, train_knn_, train_dist)


if __name__ == "__main__":
    load_vec()