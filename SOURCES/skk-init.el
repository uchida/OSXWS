;;
;; skk-init.el
;;
;; 	for OSXWS with emacsen-common
;; 	Munehiro Yamamoto <munepi@cg8.so-net.ne.jp>

(defcustom osxws-default-skk t
  "A boolean for osxws-default-skk"
  :type 'boolean)

(add-hook 'osxws-default-setup-hook
	  (lambda()
	    (if osxws-default-skk
		(require 'osxws-default-skk))))

;;; end of file
