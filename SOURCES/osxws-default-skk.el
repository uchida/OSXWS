;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;  -*- coding: utf-8-unix -*-
;;  FSF Emacs 23 用  Linux SKK 設定
;;    Akuhiro Uchida <uchida@ike-dyn.ritsumei.ac.jp>
;;    Original Author: Munehiro Yamamoto <munepi@cg8.so-net.ne.jp>
;;	$Id: osxws-default-skk.el,v 1.1 2011/10/22 12:00:56 uchida Exp $	
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; SKK-9.6m 
;;   Mule 上の仮名漢字変換システム SKK の設定
;;   C-x t でチュートリアルが起動します
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(if (equal emacs-ime "skk")
    (progn
;;;;;;;;;; 使用する辞書の設定 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; SKK-JISYO.L をメモリ上に読み込んで利用する場合
(setq skk-large-jisyo "/usr/osxws/share/skk/SKK-JISYO.L")

;;; SKK-JISYO.M をメモリ上に読み込み、
;;; 見付からない場合は skkserv を起動して SKK-JISYO.L から検索する場合
;;; (skkexdic パッケージが必要です)
;;(setq skk-large-jisyo "/usr/osxws/share/skk/SKK-JISYO.M")
;;(setq skk-aux-large-jisyo "/usr/osxws/share/skk/SKK-JISYO.L")
;;(setq skk-server-portnum 1178)
;;(setq skk-server-host "localhost")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(global-set-key "\C-x\C-j" 'skk-mode)
(global-set-key "\C-xj" 'skk-auto-fill-mode)
(global-set-key "\C-xt" 'skk-tutorial)
(autoload 'skk-mode "skk" nil t)
(autoload 'skk-auto-fill-mode "skk" nil t)
(autoload 'skk-tutorial "skk-tut" nil t)
(autoload 'skk-isearch-mode-setup "skk-isearch" nil t)
(autoload 'skk-isearch-mode-cleanup "skk-isearch" nil t)
(add-hook 'isearch-mode-hook
	  (function (lambda ()
		      (and (boundp 'skk-mode) skk-mode
			   (skk-isearch-mode-setup) ))))
(add-hook 'isearch-mode-end-hook
	  (function (lambda ()
		      (and (boundp 'skk-mode) skk-mode
			   (skk-isearch-mode-cleanup)
			   (skk-set-cursor-color-properly) ))))

))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(provide 'osxws-default-skk)

;; Local Variables:
;; mode: emacs-lisp
;; End:
